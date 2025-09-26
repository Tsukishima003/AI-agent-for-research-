import PQueue from "p-queue";
export class RateLimiter {
    queue;
    constructor(options) {
        this.queue = new PQueue({
            concurrency: options?.concurrency ?? 4,
            intervalCap: options?.intervalCap ?? 10,
            interval: options?.interval ?? 1000,
            carryoverConcurrencyCount: true,
            autoStart: true,
        });
    }
    async schedule(task) {
        return this.queue.add(task);
    }
}
//# sourceMappingURL=rateLimiter.js.map