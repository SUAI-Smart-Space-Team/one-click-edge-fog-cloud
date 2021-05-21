pipeline 
{
    agent 
    {
       label 'Deploy2'
    }
    stages 
    {
        stage("building")
        {
            steps
            {
                sh 'python3 main.py $configurator $module $action'
            }
        }
    }
}
