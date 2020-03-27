import unity_python.client.unity_client as unity_client


class SimpleTestClientService(unity_client.UnityClientService):
    def exposed_client_name(self):
        return "This is my first unity tool."


if __name__ == '__main__':
    service = SimpleTestClientService()
    connect = unity_client.connect(service)
    UnityEngine = service.UnityEngine

    geo = UnityEngine.GameObject.CreatePrimitive(UnityEngine.PrimitiveType.Cylinder)
    geo.name = "myCylinder"
    # connect.close()
