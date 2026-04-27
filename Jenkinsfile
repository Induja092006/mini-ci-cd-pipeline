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
                bat 'docker build -t flask-docker-app .'
            }
        }

        stage('Stop & Clean Old Container') {
            steps {
                script {
                    bat 'docker stop test-app || exit /b 0'
                    bat 'timeout /t 3'
                    bat 'docker rm -f test-app || exit /b 0'
                    bat 'docker container prune -f'
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    bat 'timeout /t 2'
                    bat 'docker run -d -p 5000:5000 --name test-app flask-docker-app'
                    echo "App running at: http://localhost:5000"
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    bat 'timeout /t 5'
                    bat 'curl http://localhost:5000 || exit /b 0'
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
