pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat 'docker build -t flask-docker-app .'
                }
            }
        }

        stage('Run App') {
            steps {
                script {
                    // Remove old container if exists
                    bat 'docker rm -f test-app || exit /b 0'

                    // Run new container
                    bat 'docker run -d -p 5000:5000 --name test-app flask-docker-app'

                    // Print info
                    echo "App is running at: http://localhost:5000"
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
