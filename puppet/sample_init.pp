class cisco_onep::vlan {
  cisco_vlan { "$::hostname 20":
    ensure => present,
    vlan_name => "puppetManaged_STORAGE_VLAN-20",
    state => active
  }
}

class cisco_onep::vlan {
  cisco_vlan { "$::hostname 22":
    ensure => present,
    vlan_name => "puppetManaged_STORAGE_VLAN-22",
    state => active
  }
}

class cisco_onep::vlan {
  cisco_vlan { "$::hostname 21":
    ensure => present,
    vlan_name => "puppetManaged_ACCESS_VLAN-21",
    state => active
  }
}

class cisco_onep::interface {
  cisco_interface { "$::hostname Ethernet1/8":
  switchport => 'access',
  description => '',
  access_vlan => 21
  }
}

class cisco_onep::interface {
  cisco_interface { "$::hostname Ethernet1/9":
  switchport => 'access',
  description => 'Description set by puppet interface resource',
  state => 'stopped'
  }
}

class cisco_onep::ospf_set {
  cisco_ospf { "$::hostname test":
    ensure => present,
  }

  cisco_interface_ospf { "$::hostname Ethernet1/33 test":
    ensure => present,
    area => "200",
  }
}

class cisco_onep::command_config {
  cisco_command_config { "$::hostname Ethernet1/10":
    command => "
              interface ethernet 1/10\n
                description Puppet Managed - Using Command Config\n
              end\n"
  }
}

class cisco_onep::command_config {
  cisco_command_config { "$::hostname Ethernet1/11":
    command => "
              interface ethernet 1/11\n
                description Puppet Managed - Command Config\n
              end\n"
  }
}

class cisco_onep::vrf_set {
    cisco_command_config { "$::hostname JP":
        command => "
                  vrf context Enterprise\n
                  ip route 192.0.8.0/24 Ethernet1/3 192.0.8.1
                  end\n"
    }
}

