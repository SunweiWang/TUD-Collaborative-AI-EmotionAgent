from matrx.logger.logger import GridWorldLogger
from matrx.grid_world import GridWorld

class ActionLogger(GridWorldLogger):
    '''
    Logger for saving the actions of all agents during each tick of the task.
    '''
    def __init__(self, save_path="", file_name_prefix="", file_extension=".csv", delimiter=";"):
        super().__init__(save_path=save_path, file_name=file_name_prefix, file_extension=file_extension, delimiter=delimiter, log_strategy=1)

    def log(self, grid_world, agent_data):
        # Create a dictionary with the log data
        log_data = {}
        # We will log score and completeness of the task
        log_data['score'] = grid_world.simulation_goal.score(grid_world)
        log_data['completeness'] = grid_world.simulation_goal.progress(grid_world)
        # For both human and agent, log their action and location per tick
        for agent_id, agent_body in grid_world.registered_agents.items():
            if 'objectadder' not in agent_id:
                log_data[agent_id + '_action'] = agent_body.current_action
                log_data[agent_id + '_location'] = agent_body.location

        # Log the number of messages sent by rescuebot and agend last tick
        log_data["human_sent_messages_nr"]=0
        log_data["rescuebot_sent_messages_nr"]=0
        tick_to_check=grid_world.current_nr_ticks - 1
        if tick_to_check in grid_world.message_manager.preprocessed_messages.keys():
            # loop through all messages of this tick
            for message in grid_world.message_manager.preprocessed_messages[tick_to_check]:

                # Log the message content for the sender and receiver
                message_content = str(message.content)

                if not message_content.startswith('Current tick') and not message_content.startswith('Our score'):
                    print(message.content, message.from_id, message.to_id)

                if message.from_id == 'human' and message.to_id == 'rescuebot':
                    log_data["human_sent_messages_nr"]+=1

                if message.from_id == 'RescueBot' and message.to_id == 'human' and not message_content.startswith('Current tick') and not message_content.startswith('Our score'):
                    log_data["rescuebot_sent_messages_nr"]+=1
                
        return log_data