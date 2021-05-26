from nameko.standalone.rpc import ClusterRpcProxy
 
CONFIG = {'AMQP_URI': 'amqp://admin:1234@127.0.0.1:5672//'}

def datasource_gateway():
    with ClusterRpcProxy(CONFIG) as rpc:
        result = rpc.manage_connections.get_datasources('B_RATING')
        return result

print(datasource_gateway())

