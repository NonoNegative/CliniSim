from shared.linked_list import LinkedList

# Global linked list object
dll = LinkedList()
dll.append(['Simulation Started'])

dll_expected = [['Simulation Started'], ["Checked Patient's Vitals"], ['Viewed Patient Profile'], ['Physical Assessment', 'Examined the patient'], ['Analyzed X-Ray Results', 'Scoliosis (20 degrees)'], ['Analyzed Bimicroscopy Results', 'Ectopia Lentis'], ['Analyzed Echocardiogram Results', 'Aortic root dilation'], ['Analyzed MRA Results', 'Left ventricular dilation'], ['Prescribed Enalapril', '20 mg | Once Daily (OD)'], ['Prescribed Losartan', '50 mg | Twice Daily (BID)'], ['Correctly Diagnosed', 'Marfan Syndrome']]