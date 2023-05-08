import TasksDestroyer from './consumer'

const consumer = new TasksDestroyer()
consumer.startConsumer().catch((error) => {
    console.error(error)
})
