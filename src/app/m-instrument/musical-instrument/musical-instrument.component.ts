import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { FilterService, MenuItem } from 'primeng/api';
import { PMetalService } from '../../p-metal.service';
import { Table } from 'primeng/table'; 
import { instrument } from 'src/interface/instrument';

@Component({
  selector: 'app-musical-instrument',
  templateUrl: './musical-instrument.component.html',
  styleUrls: ['./musical-instrument.component.css']
})
export class MusicalInstrumentComponent implements OnInit {
  items: MenuItem[] | undefined;

  instruments: instrument[] = [];
  filteredInstruments: instrument[] = [];
  suppliers!: any[];
  selectedSuppliers: string[] = [];
  brands!: any[];
  selectedBrands: string[] = [];

  home: MenuItem | undefined;

  loading: boolean = true;
  onFilter: boolean = false;

  constructor(private filterService: FilterService,
    private dialog: MatDialog,
    private pMetalService: PMetalService) { }

  ngOnInit(): void {
    this.items = [{ label: 'Inventory', routerLink: '/minstrument/inventory' }];

    this.home = { icon: 'pi pi-home', routerLink: '/home' };

    this.loadInstruments();

    this.filteredInstruments = this.instruments;

    this.loading = false;
  }

  loadInstruments(): void {
    this.pMetalService.getInstruments()
      .subscribe(instruments => {
        this.instruments = instruments
        this.instruments.forEach(instruments => instruments.delete = false);
        const uniqueValues = Array.from(new Set(this.instruments.map(instrument => instrument.supplierName)));
        this.suppliers = uniqueValues;
        const uniqueValues2 = Array.from(new Set(this.instruments.map(instrument => instrument.brand)));
        this.brands = uniqueValues2;

        console.log(this.instruments);
      });
  }

  clearFilter() {
    //this.selectedUnits = [];
    //this.selectedMetals = [];
    //this.selectedCategory = [];
  }

  editInstrument(instrument: any): void {
    //this.pMetalService.getProduct(product.productID)
    //  .subscribe(product => {
    //    this.productToEdit = product;

    //    const images = [];
    //    if (product.images) {
    //      for (const image of product.images) {
    //        images.push(image);
    //      }
    //    }
    //    this.openModal2(true);
    //  });
  }

  deleteInstrument(instrumentID: number) {
    const index = this.instruments.findIndex(instrument => instrument.instrumentID === instrumentID);
    this.instruments[index].delete = false;
    const instrument = this.instruments[index];
  }

  confirmDelete(instrumentID: number) {
    const index = this.instruments.findIndex(instrument => instrument.instrumentID === instrumentID);
    if (index !== -1) {
      this.instruments[index].delete = true;
    }
  }

  cancelDeleteInstrument(instrumentID: number): void {
    const index = this.instruments.findIndex(instrument => instrument.instrumentID === instrumentID);
    if (index !== -1) {
      this.instruments[index].delete = false;
    }
  }

  search(table: Table, event: any) {
    const targetValue = event.target.value;
    table.filterGlobal(targetValue, 'contains');
  }

  clickFilter(): void {
    if (this.onFilter) {
      this.onFilter = false;
    } else {
      this.onFilter = true;
    }
  }

  clear(table: Table) {
    table.clear();
    this.selectedSuppliers = [];
    this.selectedBrands = [];
  }
}
