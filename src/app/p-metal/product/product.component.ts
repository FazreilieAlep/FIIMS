import { Component, NgModule, OnInit } from '@angular/core';
import { PMetalService } from 'src/app/p-metal.service';
import { pmetal } from 'src/interface/pmetal';
import { MenuItem } from 'primeng/api';
import { MatDialog } from '@angular/material/dialog';
import { CreateOrEditProductComponent } from 'src/app/p-metal/create-or-edit-product/create-or-edit-product.component'
import { pmetal_details } from '../../../interface/pmetal-details';
import { FilterService } from 'primeng/api';
import { Table } from 'primeng/table';


export interface Metal {
  name: string,
  image: string
}
@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.css']
})

export class ProductComponent implements OnInit {

  productToEdit: pmetal_details | undefined;
  products: pmetal[] = [];
  filteredProducts: any[] = [];
  goldPrice = 317.74;
  modalOpened = false;
  modalOpened2 = false;
  createProduct = false;
  loading: boolean = true;
  onFilter: boolean = false;

  items: MenuItem[] | undefined;

  home: MenuItem | undefined;

  metals: any[] = ['gold','silver'];
  selectedMetals: string[] = [];

  units: any[] = ['oz', 'g', 'kg'];
  selectedUnits: string[] = [];

  category: any[] = ['coin', 'bar'];
  selectedCategory: string[] = [];

  suppliers!: any[];
  selectedSuppliers: string[] = [];

  constructor(
    private filterService: FilterService,
    private dialog: MatDialog,
    private pMetalService: PMetalService) { } // Inject PMetalService


  ngOnInit(): void {
    this.items = [{ label: 'Inventory', routerLink: '/pmetal/inventory' }];

    this.home = { icon: 'pi pi-home', routerLink: '/home' };

    this.loadProducts(); // Call the method to load products when the component initializes

    this.filteredProducts = this.products;

    this.loading = false;
  }

  loadProducts(): void {
    this.pMetalService.getProducts()
      .subscribe(products => {
        this.products = products
        this.products.forEach(product => product.delete = false);
        const uniqueValues = Array.from(new Set(this.products.map(product => product.supplierName)));
        this.suppliers = uniqueValues;
      });
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

  openModal2(toEdit: boolean): void {
    if (this.modalOpened2 == false) {
      if (toEdit == true) {
        this.createProduct = false;
      } else {
        this.createProduct = true;
      }
      this.modalOpened2 = true;
    }
  }

  closeModal(): void {
    if (this.modalOpened2 == true) {
      this.modalOpened2 = false;
    }
  }

  editProduct(product: pmetal): void {
    this.pMetalService.getProduct(product.productID)
      .subscribe(product => {
        this.productToEdit = product;

        const images = [];
        if (product.images) {
          for (const image of product.images) {
            images.push(image);
          }
        }
        this.openModal2(true);
      });
  }

  confirmDelete(productID: number): void {
    //console.log(productID);
    const index = this.products.findIndex(product => product.productID === productID);
    if (index !== -1) {
      this.products[index].delete = true;
    }
  }

  deleteProduct(productID: number): void {
    const index = this.products.findIndex(product => product.productID === productID);
    this.products[index].delete = false;
    const product = this.products[index];

    this.pMetalService.deleteProduct(product).subscribe(() => {
      // On successful deletion, reload the products list to synchronize
      this.loadProducts();
      alert(product.productName + ' deleted');
    });
  }

  cancelDeleteProduct(productID: number): void {
    const index = this.products.findIndex(product => product.productID === productID);
    if (index !== -1) {
      this.products[index].delete = false;
    }
  }

  clickFilter(): void {
    if (this.onFilter) {
      this.onFilter = false;
    } else {
      this.onFilter = true;
    }
  }

  clearFilter() {
    this.selectedUnits = [];
    this.selectedMetals = [];
    this.selectedCategory = [];
  }

  clear(table: Table) {
    table.clear();
  }

  search(table: Table, event: any) {
    const targetValue = event.target.value;
    table.filterGlobal(targetValue, 'contains');
  }

  onInputChange(event: any) {
    const targetValue = event;
     // Access the value of the target element
    console.log('Target value:', targetValue);
    // You can perform further actions based on the target value
  }

  getName(event: any) {
    const targetValue = event.map((item: { name: any; }) => item.name);
    return targetValue
  }
}
