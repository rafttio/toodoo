import knex, {Knex} from "knex";

export default class Tasks {
    private dbClient: Knex

    public constructor() {
        this.dbClient = Tasks.createDBClient()
    }

    public async deleteTask(taskId: number) {
        try {
            console.log(`Deleting task: ${taskId}`)
            await this.dbClient('tasks').where('id', taskId).del()
        } catch (error) {
            console.log('Error: ', error)
        }
    }

    public async shutdown(): Promise<void> {
        await this.dbClient.destroy()
    }

    private static createDBClient(): Knex {
        return knex({
            client: 'pg',
            connection: {
                'connectionString': process.env.DATABASE_URL
            }
        });
    }
}
