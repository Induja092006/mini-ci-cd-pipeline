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

        stage('Stop & Remove Old Container') {
            steps {
                script {
                    // Stop container if running (ignore errors)
                    bat 'docker stop test-app || exit /b 0'

                    // Force remove container (important fix for your error)
                    bat 'docker rm -f test-app || exit /b 0'
                }
            }
        }

        stage('Run App') {
            steps {
                script {
                    // Run new container safely
                    bat 'docker run -d -p 5000:5000 --name test-app flask-docker-app'

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
