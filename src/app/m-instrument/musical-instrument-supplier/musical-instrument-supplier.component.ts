import { Component, OnInit } from '@angular/core';
import { supplier } from '../../../interface/supplier';
import { MenuItem, MessageService } from 'primeng/api';
import { PMetalService } from '../../p-metal.service';
import { Table } from 'primeng/table';

@Component({
  selector: 'app-musical-instrument-supplier',
  templateUrl: './musical-instrument-supplier.component.html',
  styleUrls: ['./musical-instrument-supplier.component.css'],
  providers: [MessageService]
})
export class MusicalInstrumentSupplierComponent{
  suppliers: supplier[] = [];

  items: MenuItem[] | undefined;

  home: MenuItem | undefined;

  newSupplierName: string = '';

  creating: boolean = false;

  clonedSuppliers: { [s: number]: any } = {};

  delete: boolean = false;

  constructor(private pMetalService: PMetalService, private messageService: MessageService) { } // Inject PMetalService

  ngOnInit(): void {
    this.items = [{ label: 'Inventory', routerLink: '/minstrument/inventory' }, { label: 'Supplier' }];

    this.home = { icon: 'pi pi-home', routerLink: '/home' };

    this.loadSuppliers(); // Call the method to load products when the component initializes

  }

  loadSuppliers(): void {
    this.pMetalService.getInstrumentSuppliers()
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
      this.pMetalService.deleteInstrumentSupplier({ supplierName: supplier.supplierName, supplierID: supplier.supplierID })
        .subscribe(() => {
          alert('OK');
          this.loadSuppliers();
        });

      this.delete = false;
    } else {
      //console.log("updating");
      if (supplier.supplierName) {
        this.pMetalService.updateInstrumentSupplier({ update_columns: ["supplierName", "address"], supplierName: supplier.supplierName, supplierID: supplier.supplierID , address: supplier.address })
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
      this.pMetalService.addInstrumentSupplier({ supplierName: this.newSupplierName })
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
