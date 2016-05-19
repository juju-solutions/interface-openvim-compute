from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class RequiresOpenVIMCompute(RelationBase):
    scope = scopes.GLOBAL

    auto_accessors = ['user', 'ssh_key_installed']

    @hook('{requires:openvim-compute}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.connected')
        if self.connection() and self.ssh_key_installed():
            self.set_state('{relation_name}.available')

    @hook('{requires:openvim-compute}-relation-{broken,departed}')
    def departed(self):
        self.remove_state('{relation_name}.connected')
        self.remove_state('{relation_name}.available')

    def send_ssh_key(self, key):
        conv = self.conversation()
        conv.set_remote('ssh_key', key)

    def address(self):
        conv = self.conversation()
        return conv.get_remote('private-address')

    def connection(self):
        user = self.user()
        address = self.address()
        return address and user
