
public class TextStripperForData {

	public static void main(String [ ] args){
		
		String my = "g_id,assignment_id^M2,13^M5,7^M9,7^M11,5^M15,6^M19,2^M20,14^M22,15^M26,9^M27,1^M28,10^M29,3^M31,4^M36,11^M37,12^M38,15^M39,8";
		my = my.replace("^M", "\n");
		System.out.println(my);
		
	}
	
}
