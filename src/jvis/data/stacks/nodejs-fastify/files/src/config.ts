import { FastifyServerOptions } from 'fastify';

export interface AppConfig {
  port: number;
  host: string;
  logLevel: string;
}

export function loadConfig(): AppConfig {
  return {
    port: parseInt(process.env.PORT || '3000', 10),
    host: process.env.HOST || '0.0.0.0',
    logLevel: process.env.LOG_LEVEL || 'info',
  };
}

export function buildFastifyOpts(): FastifyServerOptions {
  return {
    logger: {
      level: loadConfig().logLevel,
    },
  };
}
