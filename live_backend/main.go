package main

import (
	"context"
	"errors"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/go-redis/redis/v8"
)

const (
	redisLivenessKey        = "live_set"
	secondsToRememberClient = 10
)

var redisClient *redis.Client

func init() {
	redisClient = redis.NewClient(&redis.Options{
		Addr:     os.Getenv("REDIS_URL"),
		Password: "", // no password set
		DB:       0,  // use default DB
	})
}

func getMaxScoreForLive() int64 {
	return time.Now().Unix() + secondsToRememberClient
}

func getMaxScoreForLiveStr() string {
	maxScore := getMaxScoreForLive()
	return fmt.Sprintf("%d", maxScore)
}

func getMinScoreForLiveStr() string {
	return fmt.Sprintf("%d", time.Now().Unix())
}

func cleanupLiveness() {
	for {
		_, err := redisClient.ZRemRangeByScore(context.TODO(), redisLivenessKey, "-inf", getMinScoreForLiveStr()).Result()
		if err != nil {
			log.Printf("WARN: Error while RemRange: %v", err)
		}
		time.Sleep(1 * time.Second)
	}
}

func addToLiveness(id string) error {
	log.Printf("DEBUG: zadd %s %d %s", redisLivenessKey, getMaxScoreForLive(), id)
	_, err := redisClient.ZAdd(context.TODO(), redisLivenessKey, &redis.Z{Score: float64(getMaxScoreForLive()), Member: id}).Result()
	return err
}

func getLiveness() (int64, error) {
	log.Printf("DEBUG: zcount %s %s %s", redisLivenessKey, getMinScoreForLiveStr(), getMaxScoreForLiveStr())
	val, err := redisClient.ZCount(context.TODO(), redisLivenessKey, getMinScoreForLiveStr(), getMaxScoreForLiveStr()).Result()
	if err != nil {
		return 0, err
	}

	return val, nil
}

func handleLive(rw http.ResponseWriter, r *http.Request) error {
	id, ok := r.URL.Query()["id"]
	if !ok || len(id) != 1 {
		return errors.New("bad id in request")
	}

	if err := addToLiveness(id[0]); err != nil {
		return errors.New("failed to add to liveness")
	}

	val, err := getLiveness()
	if err != nil {
		return errors.New("failed to get liveness")
	}

	rw.Header().Set("Access-Control-Allow-Origin", "*")
	rw.Write([]byte(fmt.Sprintf("%d", val)))
	return nil
}

func main() {
	go cleanupLiveness()
	http.HandleFunc("/live", func(rw http.ResponseWriter, r *http.Request) {
		if err := handleLive(rw, r); err != nil {
			http.Error(rw, err.Error(), http.StatusInternalServerError)
		}
	})

	panic(http.ListenAndServe(":3001", nil))
}
