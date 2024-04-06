import boto3
import time

def update_ecs_service(cluster_name, service_name, new_task_definition_arn, desired_count):
    ecs_client = boto3.client('ecs')
    
    # Step 1: Update service to desired count of 0
    ecs_client.update_service(
        cluster=cluster_name,
        service=service_name,
        desiredCount=0
    )
    
    # Step 2: Update service to use new task definition
    ecs_client.update_service(
        cluster=cluster_name,
        service=service_name,
        taskDefinition=new_task_definition_arn
    )
    
    # Step 3: Scale up service to desired count
    ecs_client.update_service(
        cluster=cluster_name,
        service=service_name,
        desiredCount=desired_count
    )
    
    # Wait for new tasks to start and pass health checks
    wait_for_tasks_to_start(cluster_name, service_name, desired_count, ecs_client)
    
    # Step 5: Terminate old tasks
    terminate_old_tasks(cluster_name, service_name, ecs_client)
    
def wait_for_tasks_to_start(cluster_name, service_name, desired_count, ecs_client):
    print("Waiting for new tasks to start...")
    while True:
        response = ecs_client.describe_services(
            cluster=cluster_name,
            services=[service_name]
        )
        running_count = response['services'][0]['runningCount']
        if running_count >= desired_count:
            print("New tasks have started.")
            break
        time.sleep(5)  # Wait for 5 seconds before checking again

def terminate_old_tasks(cluster_name, service_name, ecs_client):
    print("Terminating old tasks...")
    response = ecs_client.list_tasks(
        cluster=cluster_name,
        serviceName=service_name,
        desiredStatus='RUNNING'
    )
    if 'taskArns' in response:
        task_arns = response['taskArns']
        ecs_client.stop_tasks(
            cluster=cluster_name,
            taskArns=task_arns
        )
        print("Old tasks terminated.")

# Example usage
if __name__ == "__main__":
    cluster_name = 'new-cluster'
    service_name = 'new-service'
    new_task_definition_arn = 'arn:aws:ecs:eu-west-2:440094375133:task-definition/new-taskdefinition:1'
    desired_count = 3  # Number of tasks you want to run with the new task definition
    update_ecs_service(cluster_name, service_name, new_task_definition_arn, desired_count)
