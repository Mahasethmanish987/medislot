pipeline {
    agent any

    environment {
        // Customize these to match your project
        IMAGE_NAME = 'my-app'
        IMAGE_TAG = 'latest'
        COMPOSE_FILE = 'docker-compose.prod.yml'
        PROJECT_NAME = 'myapp'   // Used for docker-compose project isolation
    }

    stages {
       

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image using the Dockerfile in the repo root
                    docker.build("${IMAGE_NAME}:${IMAGE_TAG}", ".")
                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                script {
                    // Bring down existing containers (optional, but ensures clean state)
                    sh "docker-compose -f ${COMPOSE_FILE} -p ${PROJECT_NAME} down --remove-orphans || true"

                    // Bring up new containers in detached mode
                    // This will use the image we just built (if compose references it)
                    sh "docker-compose -f ${COMPOSE_FILE} -p ${PROJECT_NAME} up -d"
                }
            }
        }
    }

    post {
        failure {
            // Optional: send notifications or log errors
            echo "Pipeline failed! Check the logs."
        }
        success {
            echo "Deployment successful! New containers are up."
        }
    }
}