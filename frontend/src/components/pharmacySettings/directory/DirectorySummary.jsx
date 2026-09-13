import PharmacyInfoCard from "./PharmacyInfoCard";
import OwnerInfoCard from "./OwnerInfoCard";
import ContactAddressCard from "./ContactAddressCard";
import LicenseCards from "./LicenseCards";

const DirectorySummary = () => (
  <>
    <section className="grid grid-cols-1 gap-4 lg:grid-cols-12">
      <div className="lg:col-span-4">
        <PharmacyInfoCard />
      </div>
      <div className="lg:col-span-4">
        <OwnerInfoCard />
      </div>
      <div className="lg:col-span-4">
        <ContactAddressCard />
      </div>
    </section>

    <LicenseCards />
  </>
);

export default DirectorySummary;