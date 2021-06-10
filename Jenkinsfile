pipeline 
{
    agent 
    {
       label 'ocefc'
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
