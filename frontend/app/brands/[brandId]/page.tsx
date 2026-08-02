import { BrandDetail } from "@/components/brand/brand-detail";

export default function BrandPage({ params }: { params: { brandId: string } }) {
  return <BrandDetail brandId={parseInt(params.brandId)} />;
}
