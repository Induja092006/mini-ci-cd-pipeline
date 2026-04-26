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

        stage('Test Container') {
            steps {
                script {
                    try {
                        bat 'docker run -d -p 5000:5000 --name test-app flask-docker-app'
                        // Wait for app to start
                        bat 'timeout /t 5 /nobreak'
                        bat 'curl http://localhost:5000'
                    } finally {
                        bat 'docker stop test-app || exit /b 0'
                        bat 'docker rm test-app || exit /b 0'
                    }
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
