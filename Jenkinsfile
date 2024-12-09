pipeline {
    // Uncomment this section if you'd like to use a different agent configuration
    // agent {
    //     node {
    //         label 'docker_agent_python'
    //     }
    // }

    agent {
        node {
            label 'my-host-agent' // Use the label assigned in the configuration
        }
    }

    triggers {
        pollSCM '*/1 * * * *'
    }

    environment {
        DOCKER_IMAGE = 'faroukcha69/ci_image'
    }

    stages {
        stage('Clone repository') {
            steps {
                checkout scm
            }
        }

        stage('Build image') {
            steps {
                script {
                    // Declare and initialize `app` inside the script block
                    def app = docker.build("${DOCKER_IMAGE}")
                    
                    // Save `app` for use in later stages by using a global environment variable
                    env.DOCKER_IMAGE_ID = app.imageName()
                }
            }
        }

        stage('Test image') {
            steps {
                script {
                    // Reuse the Docker image saved in the environment variable
                    def app = docker.image("${env.DOCKER_IMAGE_ID}")
                    app.inside {
                        sh 'echo "Tests passed"'
                    }
                }
            }
        }

        stage('Push image') {
            steps {
                script {
                    // Reuse the Docker image saved in the environment variable
                    def app = docker.image("${env.DOCKER_IMAGE_ID}")
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
                        app.push("${env.BUILD_NUMBER}")
                    }
                }
            }
        }

        stage('Trigger ManifestUpdate') {
            steps {
                build job: 'cd_update_manifest_job', 
                    parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER)]
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }

        success {
            echo 'Pipeline succeeded!'
        }

        failure {
            echo 'Pipeline failed!'
        }

        // Uncomment this section if you want to include cleanup logic
        // cleanup {
        //     script {
        //         // Optional cleanup logic, e.g., remove unused Docker images
        //         sh 'docker image prune -f'
        //     }
        // }
    }
}
