import csv,json


class bot_config:
    def __init__(self):
        self.config_name = 'ta_standard'
        self.take_profit = 1.5
        self.base_order=10
        self.safety_order=20
        self.max_safety_orders = 30
        self.deviation_to_open_safety_order = 2.0
        self.safety_order_volume_scale = 1.05
        self.safety_order_step_scale = 1
    def to_json(self):
        return json.dumps(self.__dict__)

class my_own_config:
    def __init__(self):
        self.config_name = 'euphoria'
        self.take_profit = 1.25
        self.base_order=10
        self.safety_order=10
        self.max_safety_orders = 8
        self.deviation_to_open_safety_order = 1.5
        self.safety_order_volume_scale = 1.75
        self.safety_order_step_scale = 1.36
    def to_json(self):
        return json.dumps(self.__dict__)

def getMax(config):
    deviation = config.deviation_to_open_safety_order
    max_safety_order_price_deviation =  deviation
    max_amount_for_bot_usage = config.base_order
    i = 1
    while i <= config.max_safety_orders:
        if i == 1:
            max_amount_for_bot_usage = max_amount_for_bot_usage + config.safety_order
            safety_order = config.safety_order * config.safety_order_volume_scale
        else:
            max_amount_for_bot_usage = max_amount_for_bot_usage + safety_order
            safety_order = safety_order * config.safety_order_volume_scale
            deviation = deviation * config.safety_order_step_scale
            max_safety_order_price_deviation = max_safety_order_price_deviation + deviation

        i+=1
    return round(max_safety_order_price_deviation,2),round(max_amount_for_bot_usage)

def readConfigs(file_name):
    config_list = []
    with open(file_name, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='|')
        header_found=False
        for row in data:
            if row[0]=='INDEX':
                header_found=True
                continue
            if header_found:
                config = bot_config()
                config.config_name = row[2].lower().strip().replace(' ','_').replace('/','_').replace('(','_').replace(')','_')
                config.take_profit = float(row[3].replace('%',''))
                config.base_order=float(row[4].replace('$',''))
                config.safety_order=float(row[5].replace('$',''))
                config.max_safety_orders = int(row[9])
                config.deviation_to_open_safety_order = float(row[8].replace('%',''))
                config.safety_order_volume_scale = float(row[6])
                config.safety_order_step_scale = float(row[7])
                config.max_safety_order_price_deviation,config.max_amount_for_bot_usage = getMax(config)

                #json_config = json.dumps(config.__dict__)

                #add to config_list array (json formatted)
                #config_list[config.config_name] = json_config
                config_list.append(config)

    #uncomment if you have a own config to add... you could also add your config to the csv file ;-)
    config = my_own_config()
    config.max_safety_order_price_deviation,config.max_amount_for_bot_usage = getMax(config)
    config_list.append(config)

    return config_list

def getConfigsByMaxBotUsage(min,max):
    config_list=[]
    for config in getAllConfigs():
        if config.max_amount_for_bot_usage >= min and config.max_amount_for_bot_usage <=max:
            config_list.append(config)
    return config_list


def getAllConfigs():
    return (readConfigs('configs/bot_configs.csv'))

def getSingleConfig(config_name):
    for config in getAllConfigs():
        if config.config_name==config_name:
            return config
    return None
