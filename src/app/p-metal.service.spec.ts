import { TestBed } from '@angular/core/testing';

import { PMetalService } from './p-metal.service';

describe('PMetalService', () => {
  let service: PMetalService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PMetalService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
