pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                // Build and tag the image so Docker Compose can find it
                sh "docker build -t my-app:latest ."
            }
        }

        stage('Inject Environment File') {
            steps {
                // Fix credentials ID: use the correct secret name (you had 'evd-prod-file' typo)
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
        success {
            echo "✅ Deployment successful!"
        }
        failure {
            echo "❌ Deployment failed. Check logs above."
        }
    }
}