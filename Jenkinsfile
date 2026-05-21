
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    docker.build("my-app:latest", ".")
                }
            }
        }

        stage('Env File') {
            steps {
                withCredentials([file(credentialsId: 'evd-prod-file', variable: 'ENV_FILE')]) {
                    sh "cp $ENV_FILE .env.prod"
                }
            }
        }

        stage('Deploy') {
            steps {
                sh "docker compose -f docker-compose.prod.yml up -d --force-recreate"
            }
        }
    }

    post {
        success { echo "Deployed successfully" }
        failure { echo "Deployment failed" }
    }
}