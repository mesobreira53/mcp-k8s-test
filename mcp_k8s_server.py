from mcp.server.fastmcp import FastMCP
from kubernetes import client, config

mcp = FastMCP(name="k8s-server", instructions="An MCP server to interact with Kubernetes.")

def initialize_kubernetes_client():
    """
    Initializes the Kubernetes client. It tries to load in-cluster configuration
    first, and falls back to kube-config for local development.
    """
    try:
        config.load_incluster_config()
    except config.ConfigException:
        try:
            config.load_kube_config()
        except config.ConfigException:
            raise Exception("Could not configure kubernetes client")
    return client.CoreV1Api()

@mcp.tool()
def list_pods(namespace: str = "default") -> dict:
    """
    Lists pods in a given namespace.

    Args:
        namespace: The namespace to list pods from.
    """
    k8s_client = initialize_kubernetes_client()
    try:
        pod_list = k8s_client.list_namespaced_pod(namespace)
        pods = [pod.metadata.name for pod in pod_list.items]
        return {"pods": pods}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run() 