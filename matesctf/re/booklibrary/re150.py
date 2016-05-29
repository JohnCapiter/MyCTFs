import angr

passphrase = None

def fgets(state):
  global passphrase
  passphrase = state.se.BVS('passphrase', 64*8)
  # passphrase's address in stack
  addr = state.regs.rbp - 0x50
  state.memory.store(addr, passphrase)

def main():
  project = angr.Project('./booklibrary')
  state = project.factory.blank_state(addr=0x40108C)
  project.hook(0x4010C5, fgets, length=5)
  init = project.factory.path(state=state)
  pg = project.factory.path_group(init)

  pg.explore(find=0x4010F2)

  found = pg.found[0]
  num = found.state.se.any_int(passphrase)
  print "Passphrase(hex) = %s" %(hex(num)[2:-1])
  return "End"

if __name__ == '__main__':
  print(repr(main()))
