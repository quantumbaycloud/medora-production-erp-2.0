import { useState } from "react";
import { useLocation, useParams, Navigate } from "react-router-dom";

import { initialSuppliersData } from "./Suppliers";

import SupplierProfileHeader from "../../components/supplierManagement/suppliers/SupplierProfileHeader";
import SupplierOverviewCards from "../../components/supplierManagement/suppliers/SupplierOverviewCards";
import SupplierContactCard from "../../components/supplierManagement/suppliers/SupplierContactCard";
import SupplierPurchaseOrders from "../../components/supplierManagement/suppliers/SupplierPurchaseOrders";
import SupplierModal from "../../components/supplierManagement/suppliers/SupplierModal";

const SupplierInformation = () => {
  const { supplierId } = useParams();
  const location = useLocation();

  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [formData, setFormData] = useState(null);

  const supplierFromState = location.state?.supplier;
  const supplierFromList = initialSuppliersData.find(
    (supplier) => supplier.id === supplierId
  );

  const supplier = supplierFromState || supplierFromList;

  if (!supplier) {
    return <Navigate to="/suppliers" replace />;
  }

  const handleOpenEdit = () => {
    setFormData({
      name: supplier.name,
      contactPerson: supplier.contactPerson,
      email: supplier.email,
      phone: supplier.phone,
      category: supplier.category,
      address: supplier.address,
      paymentTerms: supplier.paymentTerms,
      gstin: supplier.gstin,
      status: supplier.status,
      description: supplier.description
    });
    setIsEditModalOpen(true);
  };

  const handleSaveEdit = (e) => {
    e.preventDefault();
    setIsEditModalOpen(false);
  };

  return (
    <div className="space-y-6 pb-12">
      <SupplierProfileHeader supplier={supplier} onEditClick={handleOpenEdit} />

      <SupplierOverviewCards supplier={supplier} />

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">
        <div className="xl:col-span-1">
          <SupplierContactCard supplier={supplier} />
        </div>

        <div className="xl:col-span-2">
          <SupplierPurchaseOrders supplier={supplier} />
        </div>
      </div>

      {formData && (
        <SupplierModal
          isOpen={isEditModalOpen}
          onClose={() => setIsEditModalOpen(false)}
          title="Manage Supplier Profile"
          subtitle="Update operational contact, status, and terms."
          onSubmit={handleSaveEdit}
          formData={formData}
          setFormData={setFormData}
          submitLabel="Save Changes"
        />
      )}
    </div>
  );
};

export default SupplierInformation;
