// this pipeline contains a few plugin dependencies you need to resolve on Jenkins:
// - sshCommand
// - ansiColor
// you also need to point Jenkins to Terraform (validated with 0.11.latest)
// you need to create a username/password credentials set that sshCommand will use
// that's about it - enjoy!

void slackTalk(msg) {
    // if you want to use Slack, add an integration (webhook-type) to your channel
    // you will receive values for T, B and S
    T = "TQD55T6UF"
    B = "BQ0K1GBGB"
    S= "oVbsstox4mp30MKNgI28d6NR"
    sh "curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"${msg}\"}' https://hooks.slack.com/services/$T/$B/$S"
}


pipeline {
 agent any
 
 stages {
   stage('Git code checkout'){
     steps {
       dir('dev'){
         ansiColor('xterm'){
           git branch: 'master', url: 'http://10.67.185.80/cisco/camrossi/cicd.git'
         }
       }
     }
   }
 

    stage('Generate  ACI Config') {
     steps {
         dir('dev/ACI'){
             ansiColor('xterm') {
                 fileOperations([fileDeleteOperation(
                     excludes: '',
                     includes: 'config.json'
                     )])
                 ansiblePlaybook(
                     playbook: './full_aci_demo.yaml',
                     inventory: './inventory',
                     extras: '--check -vvv',
                     colorized: true)
                    }

       }
     }
    }
    
    stage('Verify ACI Config') {
     steps {
         dir('dev/ACI'){
             ansiColor('xterm') {
                 sh 'pip3 install -r requirements.txt'
                 ansiblePlaybook(
                     playbook: './nae_pcv.yaml',
                     inventory: './inventory',
                     extras: '-vvv',
                     colorized: true)
                    }

       }
     }
    }

    stage('Push ACI Config') {
     steps {
       dir('dev/ACI'){
             ansiColor('xterm') {
                 ansiblePlaybook(
                     playbook: './full_aci_demo.yaml',
                     inventory: './inventory',
                     extras: '-vvv',
                     colorized: true) 
                    }

       }
     }
    }
   
  }
}
