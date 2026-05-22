pipeline {
    agent any
    environment {
        APP_DIR = 'doctor-appointment'   // or leave empty if repo root is workspace
    }
    stages {
        stage('Build Docker Image') {
            steps {
                dir(env.APP_DIR) {
                    sh "docker pull my-app:latest || true"
                    sh "docker build --cache-from my-app:latest -t my-app:latest ."
                }
            }
        }
        stage('Inject Environment File') {
            steps {
                dir(env.APP_DIR) {
                    withCredentials([file(credentialsId: 'evd-prod-file', variable: 'ENV_FILE')]) {
                        sh "cp $ENV_FILE .env.prod"
                    }
                }
            }
        }
        stage('Deploy with Compose') {
            steps {
                dir(env.APP_DIR) {
                    sh "docker compose -f docker-compose.prod.yml up -d --force-recreate --remove-orphans"
                }
            }
        }
    }
}