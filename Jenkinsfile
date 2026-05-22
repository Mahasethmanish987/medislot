pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Pull latest image for cache (ignore failure on first run)
                    sh "docker pull my-app:latest || true"
                    sh "docker build --cache-from my-app:latest -t my-app:latest ."
                }
            }
        }

        stage('Inject Environment File') {
            steps {
                withCredentials([file(credentialsId: 'evd-prod-file', variable: 'ENV_FILE')]) {
                    sh "cp $ENV_FILE .env.prod"
                }
            }
        }

        stage('Deploy with Compose') {
            steps {
                sh "docker compose -f docker-compose.prod.yml up -d --force-recreate --remove-orphans"
            }
        }
    }

    post {
        success { echo "✅ Deployment successful!" }
        failure { echo "❌ Deployment failed. Check logs above." }
    }
}