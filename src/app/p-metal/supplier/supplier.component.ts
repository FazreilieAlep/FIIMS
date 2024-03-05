import { Component } from '@angular/core';
import { supplier } from 'src/interface/supplier'
import { PMetalService } from 'src/app/p-metal.service'
import { MenuItem } from 'primeng/api';

@Component({
  selector: 'app-supplier',
  templateUrl: './supplier.component.html',
  styleUrls: ['./supplier.component.css']
})
export class SupplierComponent {

  suppliers: supplier[] = [];
  goldPrice = 317.74;

  items: MenuItem[] | undefined;

  home: MenuItem | undefined;

  constructor(private pMetalService: PMetalService) { } // Inject PMetalService

  ngOnInit(): void {
    this.items = [{ label: 'Inventory', routerLink: '/pmetal/inventory' }, { label: 'Supplier' }];

    this.home = { icon: 'pi pi-home', routerLink: '/home' };

    this.loadSuppliers(); // Call the method to load products when the component initializes
  }

  loadSuppliers(): void {
    this.pMetalService.getSuppliers()
      .subscribe(suppliers => this.suppliers = suppliers);
  }

}
