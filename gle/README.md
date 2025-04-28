# Gamified Learning Experience (GLE)
This directory contains the source code for the gle-app and gle-web Docker images.

## Local development
If you wish to use these packages directly on a machine running the Docker engine, a .env file must be defined as per the example given by the .env.example file. Run the following command from within the gle directory to run in Docker.

```cmd
docker compose -f docker-compose-dev.yml up --build
```

The frontend is then available at [http://localhost][http://localhost].

If you wish to build and run the app without the Docker engine, you will need to install both Node.js v22.13.1 or greater and Python v3.12.1 or greater. Once installed, the .env file will need to be defined within the gle/backend directory and a copy must also exist within the gle/frontend directory. An example of an appropriate .env file for local development is given in the .env.local.example file. The frontend and backend can be run on localhost by running the following commands.

In one terminal...

```cmd
cd backend
pip install -r requirements.txt
python api.py
```

In another terminal...

```cmd
cd frontend
npm install
npm run dev
```

The frontend will then be accessible at the URL displayed in the second terminal.


## Production
In order to use the software in production, a .env file must be defined as per the example given by the .env.example file. The web app can then be spun up by running the following.

```cmd
docker compose up
```

The frontend is then available at the FRONTEND_URL defined in the .env file.
