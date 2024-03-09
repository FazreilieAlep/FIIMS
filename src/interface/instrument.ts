export interface instrument {
  instrumentID: number;
  instrumentName: string;
  supplierName: string;
  quantity?: number;
  imageLink?: string;
  brand?: string;
  variation?: string;
  price?: number;
  delete?: boolean;
}
