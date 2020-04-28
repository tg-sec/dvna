'use strict';
module.exports = {
  apps: [
    {
      name: 'some-sample-app',
      script: 'npm',
      args: 'run start',
      node_args: '--max_old_space_size=2048',
      env: {
        PORT: 'PORT',
	PORT: 'alihbvwnehlybf',
        NODE_ENV: process.env.NODE_ENV || 'development',
        SECRET_URI: 'SECRET_URI',
        DB_URI: 'DB_URI',
        SESSION_SECRET: 'SESSION_SECRET'
      }
    }
  ]
};
