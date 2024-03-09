import { ChangeDetectorRef, Component, Input, OnInit } from '@angular/core';
import { PMetalService } from '../../p-metal.service';
import { ActivatedRoute } from '@angular/router';
import { MenuItem } from 'primeng/api';
import { Location } from '@angular/common';

@Component({
  selector: 'app-musical-instrument-details',
  templateUrl: './musical-instrument-details.component.html',
  styleUrls: ['./musical-instrument-details.component.css']
})
export class MusicalInstrumentDetailsComponent implements OnInit {
  @Input() instrument: any = {};

  images: any[] | undefined;
  responsiveOptions: any[] | undefined;
  desc?: string;
  paragraphs?: string[];

  items: any[] = [];

  home: MenuItem | undefined;

  modalOpened2 = false;
  createProduct = false;

  constructor(
    private route: ActivatedRoute,
    private pMetalService: PMetalService,
    private location: Location,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    this.items.push({ label: 'Inventory', routerLink: '/minstrument/inventory' });
    this.items.push({ label: 'Instrument', routerLink: '/minstrument/inventory/' + Number(this.route.snapshot.paramMap.get('id')).toString() });

    this.home = { icon: 'pi pi-home', routerLink: '/home' };

    this.responsiveOptions = [
      {
        breakpoint: '1024px',
        numVisible: 5
      },
      {
        breakpoint: '768px',
        numVisible: 3
      },
      {
        breakpoint: '560px',
        numVisible: 1
      }
    ];

    this.loadProduct();

    this.cdr.detectChanges();
  }

  loadProduct(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.pMetalService.getInstrument(id)
      .subscribe(instrument => {
        this.instrument = instrument;
        if (instrument.instrumentName) {
          this.items.push({ label: instrument.instrumentName, routerLink: '/minstrument/inventory/' + id.toString() });
          this.images = instrument.images;
          this.cdr.detectChanges();
          this.desc = instrument.desc;
          this.paragraphs = this.desc.split("\\\\n");
        }
      });
  }

}
