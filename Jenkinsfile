pipeline {
    agent any

    environment {
        // Customize these to match your project
        IMAGE_NAME = 'my-app'
        IMAGE_TAG = 'latest'
        COMPOSE_FILE = 'docker-compose.prod.yml'
        PROJECT_NAME = 'myapp'           // used for container naming and isolation
    }

    stages {
        

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the image using the Dockerfile in the repository root
                    docker.build("${IMAGE_NAME}:${IMAGE_TAG}", ".")
                }
            }
        }

        stage('Create .env.prod') {
            steps {
                // Inject the secret file (uploaded in Jenkins credentials) and copy it as .env.prod
                withCredentials([file(credentialsId: 'env-prod-file', variable: 'ENV_FILE')]) {
                    script {
                        sh "cp $ENV_FILE .env.prod"
                    }
                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                script {
                    // Single command: recreate containers with the new image
                    sh "docker-compose -f ${COMPOSE_FILE} -p ${PROJECT_NAME} up -d --force-recreate"
                }
            }
        }
    }

    post {
        failure {
            echo "Pipeline failed! Check the logs."
        }
        success {
            echo "Deployment successful! New containers are up."
        }
    }
}