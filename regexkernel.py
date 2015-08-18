import re
import sys

def kernel_count(code):
	#AI = (#add+#mul)/(#load+#store)*wordsize
	#AIw = ((#add+#mul)/2*max(#add,#mull))*AI
        ER_array = '(\w*(\[[^]]*\]){1,})'
	ER_store = '(\w*(\[[^]]*\]){1,})(?=\s*[+,\-,*,/]=)|(\w*(\[[^]]*\]){1,})(?=\s*=[^=])'	
	ER_comment = '(/\*.*?\*/|//[^\r\n]*$)'
	ER_fake_negative = '(:?=|\()\s*-'
	ER_fake_positive = '(:?=|\()\s*\+'
	ER_hidden_load = '(\w*(\[[^]]*\]){1,})(?=\s*[+,\-,*,/]=)'
	ER_add = '\+'
	ER_sub = '\-'
	ER_mul = '\*'
	ER_div = '\/'
	ER_generic = '(\w*(\[[^]]*\]){1,})|[\(\w.\)]'
        
	kernel = ''
	wordsize = 4.0 #single precision
	load = 0.0
	store = 0.0
	mul = 0.0
	add = 0.0
	sub = 0.0
	div = 0.0
	kernel_input = code
	regex_comment = re.compile(ER_comment,re.MULTILINE|re.DOTALL)
	kernel_wt_comment = regex_comment.sub('',kernel_input)
	for line in kernel_wt_comment.splitlines():
		line_wt_comment =  re.search(ER_array,line)
		if line_wt_comment:  
	             kernel+=line      
#	for line in file_kernel:
#		  line_wt_comment = re.sub(ER_comment,'',line)
#		  line_wt_array =  re.search(ER_array,line_wt_comment)
#		  if line_wt_array:  
 #        	      kernel+=line

	only_array = re.findall(ER_generic,kernel)
	only_array_wt_duplicated = set(only_array) #remove duplicated
#	print only_array_wt_duplicated
        for match in only_array_wt_duplicated:
		if not match[0] == '':
			load = load + 1.0
#		print match[0]

	hiden_load_arrays = re.findall(ER_hidden_load,kernel) #count loads in -=,+=...
        for match in hiden_load_arrays:
                load = load + 1.0
	
#	print "Load: %d" %(load)

	count_store = re.findall(ER_store,kernel) #count store
        for match in count_store:
                store = store + 1.0
	
#	print "Store: %d" %(store)

	fake_negatives = re.sub(ER_fake_negative,'',kernel) #take out - negatives
#	print fake_negatives
	fake_positives = re.sub(ER_fake_positive,'',fake_negatives) #take out fake + positives
#	print fake_positives
	count_op = re.sub(ER_generic,'',fake_positives) #only signals
#	print count_op
	all_adds = re.findall(ER_add,count_op)
        for match in all_adds:
                add = add + 1.0

        all_subs = re.findall(ER_sub,count_op)
        for match in all_subs:
                sub = sub + 1.0

        all_mults = re.findall(ER_mul,count_op)
        for match in all_mults:
                mul = mul + 1.0

        all_divs = re.findall(ER_div,count_op)
        for match in all_divs:
               div = div + 1.0
	
	result = (['load',load],['store',store],['add',add],['sub',sub],['mul',mul],['div',div])
	#print "add %d sub %d mul %d div %d" %(add,sub,mul,div)
	print result

	AI = (add+sub+mul+div)/((load+store)*wordsize)
	AIw = ((add+sub+mul+div)/(2.0*max(add+sub,mul+div)))*AI
	print "AI = %f Flops/Byte\nAIw = %f Flops/Byte\n" %(AI,AIw)

if __name__ == '__main__':
    result = kernel_count(sys.argv[1])
