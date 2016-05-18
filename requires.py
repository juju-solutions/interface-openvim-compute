from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class RequiresOpenVIMCompute(RelationBase):
    scope = scopes.UNIT

    auto_accessors = ['hostname', 'user']

    @hook('{requires:openvim-compute}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.connected')
        if self.connection():
            self.set_state('{relation_name}.available')

    @hook('{requires:openvim-compute}-relation-{broken,departed}')
    def departed(self):
        self.remove_state('{relation_name}.connected')
        self.remove_state('{relation_name}.available')

    def send_ssh_key(key):
        conv = self.conversation()
        conv.set_remote('key', key)

    def address():
        conv = self.conversation()
        return conv.get_remote('private-address')

    def list_nodes():
        for convo in self.conversations()
            yield convo

    def connection():
        hostname = self.hostname()
        user = self.user()
        address = self.address()

        return address and hostname and user
