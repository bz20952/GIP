# Gamified Learning Experience (GLE)
This directory contains the source code for the gle-app and gle-web Docker images.

If you wish to use these packages directly on a machine running the Docker engine, run the following command from within the gle directory.

```cmd
docker compose -f docker-compose-dev.yml up --build
```

If you wish to build and run the frontend without the Docker engine, you will need to install both Node.js v22.13.1 or greater and Python v3.12.1 or greater. Once installed, the .env file will need to be defined within the gle directory and a copy must also exist within the gle/frontend directory. An example of a .env file is given in the .env.example file. The frontend and backend can be run on localhost by running the following commands.

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

