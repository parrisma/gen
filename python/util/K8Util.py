from kubernetes import client, config


class K8Util:
    _k8s_config = config.load_kube_config()

    @classmethod
    def get_node_port_number(cls,
                             namespace: str = 'kafka',
                             service_name: str = 'kafka-service',
                             port_id: int = 19093) -> int:
        """
        Use kubectl to get the details of the elastic service and this teh node port assigned to elastic.
        This assumes the elastic-search service is deployed and running with the deployment as defined
        in the ./k8s-elastic dir.
        :param namespace: The Kubernetes namespace in which the service is defined
        :param service_name: The name of the service
        :param port_id: The port to find the associated NodePort id
        """
        node_port: int = None
        v1 = client.CoreV1Api()
        ret = v1.list_namespaced_service(namespace=namespace, watch=False)
        for svc in ret.items:
            if svc.metadata.name == service_name:
                for port in svc.spec.ports:
                    if port.port == port_id:
                        node_port = svc.spec.ports[0].node_port
                        break
        v1.api_client.rest_client.pool_manager.clear()
        v1.api_client.close()
        return node_port
