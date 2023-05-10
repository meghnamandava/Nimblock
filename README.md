# Nimblock 2.0
Serverless Computing with Multi-Tenant FPGAs

Serverless computing has gained significant popularity in recent years, especially in cloud computing environments. Although Field-Programmable Gate Arrays (FPGAs) have become increasingly common in cloud computing environments, there has been limited research into how FPGAs can be integrated into serverless computing frameworks to further improve performance and cost-efficiency. We propose integrating virtualized multi-tenant FPGAs into serverless platforms, enabling developers to leverage the speed and versatility of FPGAs to build and execute high-performance, customizable applications easily. Our evaluation of the Nimblock 2.0 heterogeneous serverless computing model shows that running FPGA workloads in a serverless environment results in an average overhead of only 13\%. Allocating requests to both CPU and FPGA compute resources can provide up to a 35\% performance improvement. The ability to allocate requests to different resource types can provide significant performance improvements, while considering workload characteristics and priority can further optimize performance.
  
## List of directories/files
  
- **knative_setup**: contains test scripts and yaml files used to set up functions/routes
- **nimblock-serverless-4-12.zip**: archived SDK project, containing board support packages and imported applications to run the Nimblock hypervisor and serverless endpoint.
  - **open_amp_cpp**: FPGA remote core program (runs bare-metal)
  - **amp_test_host_cpp**: FPGA host program (runs on Linux)
  
### For any questions or issues, email me (meghnam4@illinois.edu)
