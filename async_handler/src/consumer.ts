import { Consumer, ConsumerSubscribeTopics, Kafka, EachMessagePayload } from 'kafkajs'
import Tasks from './db'

export default class TasksDestroyer {
    private kafkaConsumer: Consumer
    private dbClient: Tasks

    public constructor() {
        this.kafkaConsumer = TasksDestroyer.createKafkaConsumer()
        this.dbClient = new Tasks()
    }

    public async startConsumer(): Promise<void> {
        const topic: ConsumerSubscribeTopics = {
            topics: ['deleted-tasks'],
            fromBeginning: false
        }

        while (true) {
            try {
                await this.kafkaConsumer.connect()
                break
            } catch (e) {
                console.error(e)
            }
        }

        await this.kafkaConsumer.subscribe(topic)

        await this.kafkaConsumer.run({
            eachMessage: async (messagePayload: EachMessagePayload) => {
                const { topic, partition, message } = messagePayload
                const prefix = `${topic}[${partition} | ${message.offset}] / ${message.timestamp}`
                console.log(`- ${prefix} ${message.key}#${message.value}`)
                if (message.value !== null) {
                    await this.dbClient.deleteTask(+message.value)
                }
            }
        })
    }

    public async shutdown(): Promise<void> {
        await this.kafkaConsumer.disconnect()
        await this.dbClient.shutdown()
    }

    private static createKafkaConsumer(): Consumer {
        const kafka = new Kafka({
            clientId: 'async-handler',
            brokers: [process.env.KAFKA_BOOTSTRAP_SERVER!]
        })
        return kafka.consumer({ groupId: 'async-handlers-group' })
    }
}
