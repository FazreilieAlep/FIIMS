import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProductComponent } from 'src/app/p-metal/product/product.component';
import { HomeComponent } from 'src/app/home/home.component';
import { ProductDetailsComponent } from 'src/app/p-metal/product-details/product-details.component'
import { SupplierComponent } from 'src/app/p-metal/supplier/supplier.component'
import { SupplierDetailsComponent } from 'src/app/p-metal/supplier-details/supplier-details.component'
import { MusicalInstrumentComponent } from './m-instrument/musical-instrument/musical-instrument.component';
import { MusicalInstrumentDetailsComponent } from './m-instrument/musical-instrument-details/musical-instrument-details.component';
import { MusicalInstrumentSupplierComponent } from './m-instrument/musical-instrument-supplier/musical-instrument-supplier.component';

const routes: Routes = [
  { path: 'pmetal/inventory', component: ProductComponent },
  { path: 'home', component: HomeComponent },
  { path: 'pmetal/inventory/:id', component: ProductDetailsComponent },
  { path: 'pmetal/supplier', component: SupplierComponent },
  { path: 'pmetal/supplier/:id', component: SupplierDetailsComponent },
  { path: 'minstrument/inventory', component: MusicalInstrumentComponent },
  { path: 'minstrument/inventory/:id', component: MusicalInstrumentDetailsComponent },
  { path: 'minstrument/supplier', component: MusicalInstrumentSupplierComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full' } // Default route
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
