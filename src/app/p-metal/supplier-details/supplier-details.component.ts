import { Component, OnInit } from '@angular/core';
import { PMetalService } from 'src/app/p-metal.service';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

@Component({
  selector: 'app-supplier-details',
  templateUrl: './supplier-details.component.html',
  styleUrls: ['./supplier-details.component.css']
})
export class SupplierDetailsComponent {

  supplier: any = {}

  constructor(
    private route: ActivatedRoute,
    private pMetalService: PMetalService,
    private location: Location
  ) { }

  ngOnInit(): void {
    this.loadSupplier();
  }

  loadSupplier(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.pMetalService.getSupplier(id)
      .subscribe(supplier => this.supplier = supplier);
  }

}
