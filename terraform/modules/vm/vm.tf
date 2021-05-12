resource "azurerm_network_interface" "projectnic" {
  name                = "${var.application_type}-${var.resource_type}-NIC"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group}"

  ip_configuration {
    name                          = "internal"
    subnet_id                     = "${var.subnet_id}"
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = "${var.public_ip_id}"
  }
}

resource "azurerm_linux_virtual_machine" "projectvm" {
  name                = "${var.application_type}-${var.resource_type}"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group}"
  size                = "${var.vm_size}"
  admin_username      = "adminuser"
  network_interface_ids = [
    azurerm_network_interface.projectnic.id,
  ]
  admin_ssh_key {
    username   = "adminuser"
    public_key = "${var.pub_key}"
  }
  os_disk {
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "16.04-LTS"
    version   = "latest"
  }
}
