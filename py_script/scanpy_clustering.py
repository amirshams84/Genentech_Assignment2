import sys, os
import numpy as np
import pandas as pd
import scanpy as sc


def scanpy_clustering(sample_name, h5file_Path, output_directory):
	# ##########################
	sc.settings.set_figure_params(dpi_save=300, facecolor='white')

	
	sc.settings.figdir = output_directory

	adata = sc.read_10x_h5(h5file_Path)

	adata.var_names_make_unique() 

	sc.pl.highest_expr_genes(adata, n_top=20, )


	sc.pp.filter_cells(adata, min_genes=200)
	sc.pp.filter_genes(adata, min_cells=3)


	adata.var['mt'] = adata.var_names.str.startswith('MT-')  # annotate the group of mitochondrial genes as 'mt'
	sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)


	adata = adata[adata.obs.n_genes_by_counts < 2500, :]
	adata = adata[adata.obs.pct_counts_mt < 5, :]

	sc.pp.normalize_total(adata, target_sum=1e4)

	sc.pp.log1p(adata)


	sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)


	adata = adata[:, adata.var.highly_variable]

	sc.pp.regress_out(adata, ['total_counts', 'pct_counts_mt'])

	sc.pp.scale(adata, max_value=10)


	sc.tl.pca(adata, svd_solver='arpack')


	sc.pp.neighbors(adata, n_neighbors=10, n_pcs=50)


	sc.tl.leiden(adata)


	sc.tl.paga(adata)
	sc.pl.paga(adata)  # remove `plot=False` if you want to see the coarse-grained graph
	sc.tl.umap(adata, init_pos='paga')
	sc.pl.umap(adata, color=['leiden'],save="_" + sample_name + ".png")

	results_file = output_directory + "/" + sample_name + ".h5ad"

	adata.write(results_file)

	return True



def main():
	args = sys.argv[1:]

	print(sys.argv[1:])
	if len(args) < 3:
		print("to Execute this script please provide the following in specified order")
		print("1. Sample name")
		print("2. h5 file path")
		print("3. output directory")
		print("Example: python scanpy_clustering.py my_sample /users/data/sample.h5 /users/result")
		sys.exit(2)
	else:
		pass
	
	sample_name = args[0]
	h5file_Path = args[1]
	output_dir = args[2]

	execution_flag = scanpy_clustering(sample_name, h5file_Path, output_dir)
	if execution_flag is True:
		print("execution successfull!!")
	else:
		print("execution failed.")
		print("please check generated log over here: ", output_dir + "/execution.log")
	

	return True


if __name__ == "__main__":
	main()


