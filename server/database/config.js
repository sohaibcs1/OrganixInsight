const config = {
  host: '134.197.75.35',
  port: 5432,
  username: 'new_user',
  password: '1234',
  database: 'datacollection',
}

export const connectionString = `postgres://${config.username}:${config.password}@${config.host}:${config.port}/${config.database}`;

