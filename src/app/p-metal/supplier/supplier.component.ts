import { Component } from '@angular/core';
import { supplier } from 'src/interface/supplier'
import { PMetalService } from 'src/app/p-metal.service'
import { MessageService, MenuItem } from 'primeng/api';
import { Table } from 'primeng/table';

@Component({
  selector: 'app-supplier',
  templateUrl: './supplier.component.html',
  styleUrls: ['./supplier.component.css'],
  providers: [MessageService]
})
export class SupplierComponent {

  suppliers: supplier[] = [];
  goldPrice = 317.74;

  items: MenuItem[] | undefined;

  home: MenuItem | undefined;

  newSupplierName: string = '';

  creating: boolean = false;

  clonedSuppliers: { [s: number]: any } = {};

  delete: boolean = false;

  constructor(private pMetalService: PMetalService, private messageService: MessageService) { } // Inject PMetalService

  ngOnInit(): void {
    this.items = [{ label: 'Inventory', routerLink: '/pmetal/inventory' }, { label: 'Supplier' }];

    this.home = { icon: 'pi pi-home', routerLink: '/home' };

    this.loadSuppliers(); // Call the method to load products when the component initializes

  }

  loadSuppliers(): void {
    this.pMetalService.getSuppliers()
      .subscribe(suppliers => {
        this.suppliers = suppliers
        this.suppliers.forEach(supplier => supplier.editing = false);
      });
  }

  onRowEditInit(supplier: any) {
    supplier.editing = true;
  }

  onRowDeleteInit(supplier: any) {
    if (!this.delete) {
      this.delete = true;
      supplier.editing = true;
    }
  }

  onRowEditSave(supplier: any) {
    if (this.delete) {
      alert('supplier ' + supplier.supplierName.toString() + ' will only be deleted if there are no product attached to it, if not being removed from the table, then there are still product from this supplier listed')
      this.pMetalService.deleteSupplier({ supplierName: supplier.supplierName, supplierID: supplier.supplierID })
        .subscribe(() => {
          alert('OK');
          this.loadSuppliers();
        });
      
      this.delete = false;
    } else {
      //console.log("updating");
      if (supplier.supplierName) {
        this.pMetalService.updateSupplier({ update_columns: ["supplierName"], supplierName: supplier.supplierName, supplierID: supplier.supplierID })
          .subscribe(() => {
            alert('supplier ' + supplier.supplierID.toString() + ' update');
            this.loadSuppliers();
          });

        this.messageService.add({ severity: 'success', summary: 'Success', detail: 'Product is updated' });
      } else {
        this.messageService.add({ severity: 'error', summary: 'Error', detail: 'Invalid Name' });
      }
    }
    supplier.editing = false;
  }

  onRowEditCancel(supplier: any) {
    supplier.editing = false;
    if (this.delete) {
      this.delete = false;
    }
  }

  supplierButtonClick() {
    if (this.creating) {
      this.creating = false;
    } else {
      this.creating = true;
    }
  }

  saveSupplier() {
    // save supplier api call
    if (this.newSupplierName) {
      this.pMetalService.addSupplier({ supplierName: this.newSupplierName })
        .subscribe(() => {
          alert(this.newSupplierName + ' update');
          this.newSupplierName = ''
          this.supplierButtonClick();
          this.loadSuppliers();
        });
    } else {
      alert('Please add the supplier name');
    }
  }

  search(table: Table, event: any) {
    const targetValue = event.target.value;
    table.filterGlobal(targetValue, 'contains');
  }
}
