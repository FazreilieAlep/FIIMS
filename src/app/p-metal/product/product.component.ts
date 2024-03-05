import { Component, NgModule, OnInit } from '@angular/core';
import { PMetalService } from 'src/app/p-metal.service';
import { pmetal } from 'src/interface/pmetal';
import { MenuItem } from 'primeng/api';
import { MatDialog } from '@angular/material/dialog';
import { CreateOrEditProductComponent } from 'src/app/p-metal/create-or-edit-product/create-or-edit-product.component'

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.css']
})

export class ProductComponent implements OnInit {

  products: pmetal[] = [];
  goldPrice = 317.74;
  modalOpened = false;
  modalOpened2 = false;
  createProduct = false;

  items: MenuItem[] | undefined;

  home: MenuItem | undefined;

  constructor(
    private dialog: MatDialog,
    private pMetalService: PMetalService) { } // Inject PMetalService


  ngOnInit(): void {
    this.items = [{ label: 'Inventory', routerLink: '/pmetal/inventory' }];

    this.home = { icon: 'pi pi-home', routerLink: '/home' };

    this.loadProducts(); // Call the method to load products when the component initializes
  }

  loadProducts(): void {
    this.pMetalService.getProducts()
      .subscribe(products => this.products = products);
  }

  openModal(): void {
    if (this.modalOpened == false) {
      const dialogRef = this.dialog.open(CreateOrEditProductComponent);
      this.modalOpened = true;
      dialogRef.afterClosed().subscribe(result => {
        this.modalOpened = false;
      });
    }
  }

  openModal2(): void {
    if (this.modalOpened2 == false) {
      this.modalOpened2 = true;
      this.createProduct = true;
    }
  }

  closeModal(): void {
    if (this.modalOpened2 == true) {
      this.modalOpened2 = false;
      this.createProduct = false;
    }
  }
}
