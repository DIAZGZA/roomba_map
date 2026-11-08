import logging
from roombapy import RoombaClient as ExternalRoombaClient

_LOGGER = logging.getLogger(__name__)

class RoombaClient:
    def __init__(self, host: str, username: str, password: str):
        self.host = host
        self._username = username
        self._password = password
        self._roomba = None

    async def async_connect(self):
        if self._roomba:
            return
        try:
            # Se instancia usando RoombaClient en vez de Roomba de roombapy >= 2.0
            self._roomba = ExternalRoombaClient(address=self.host, blid=self._username, password=self._password)
            await self._roomba.connect()
            _LOGGER.info("Connected to Roomba %s via RoombaClient", self.host)
        except Exception as err:
            _LOGGER.error("Failed to connect locally to Roomba %s: %s", self.host, err)
            raise

    async def async_fetch_all(self):
        await self.async_connect()
        
        # En roombapy >= 2.0 el estado maestro se obtiene desde master_state o state
        state = {}
        if hasattr(self._roomba, "master_state"):
            state = self._roomba.master_state
        elif hasattr(self._roomba, "state"):
            state = self._roomba.state

        map_png = None
        if hasattr(self._roomba, "get_map_png"):
            try:
                map_png = await self._roomba.get_map_png()
            except Exception as err:
                _LOGGER.warning("Failed to fetch map image: %s", err)

        return {"state": state, "map": map_png}
