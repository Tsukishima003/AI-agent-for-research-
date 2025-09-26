import PQueue from "p-queue";

export class RateLimiter {
  private readonly queue: PQueue;

  constructor(options?: { concurrency?: number; intervalCap?: number; interval?: number }) {
    this.queue = new PQueue({
      concurrency: options?.concurrency ?? 4,
      intervalCap: options?.intervalCap ?? 10,
      interval: options?.interval ?? 1000,
      carryoverConcurrencyCount: true,
      autoStart: true,
    });
  }

  async schedule<T>(task: () => Promise<T>): Promise<T> {
    return this.queue.add(task);
  }
}


